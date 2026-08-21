// DoWH Intranet — TipTap rich text editor (vanilla, framework-agnostic)
// Builds a self-contained toolbar + content editor and syncs HTML into a
// hidden textarea for the existing compose forms. Exposes `window.DoWHEditor`.
//
// Design tokens come from tokens.css (--ink, --dowh-gold, --border, --font-sans…).
// Image upload goes through Frappe's /api/method/upload_file so files land in
// the standard Frappe File library (no third-party storage).

import { Editor } from '@tiptap/core'
import StarterKit from '@tiptap/starter-kit'
import Link from '@tiptap/extension-link'
import Image from '@tiptap/extension-image'
import { TableKit } from '@tiptap/extension-table'
import TextAlign from '@tiptap/extension-text-align'
import Underline from '@tiptap/extension-underline'
import Placeholder from '@tiptap/extension-placeholder'
import './editor.css'

function csrfToken() {
  return (window.frappe && window.frappe.csrf_token) || ''
}

// Upload a file to Frappe and resolve to the public file URL.
function uploadFile(file) {
  const fd = new FormData()
  fd.append('file', file)
  fd.append('is_private', '0')
  const headers = {}
  const tok = csrfToken()
  if (tok) headers['X-Frappe-CSRF-Token'] = tok

  return fetch('/api/method/upload_file', { method: 'POST', headers, body: fd })
    .then((r) => {
      if (!r.ok) throw new Error('Upload failed (' + r.status + ')')
      return r.json()
    })
    .then((d) => {
      const msg = d.message || d
      const url = msg.file_url || d.file_url
      if (!url) throw new Error('Upload response missing file_url')
      return url
    })
}

function el(tag, attrs, children) {
  const node = document.createElement(tag)
  if (attrs) {
    for (const k in attrs) {
      if (k === 'class') node.className = attrs[k]
      else if (k === 'text') node.textContent = attrs[k]
      else node.setAttribute(k, attrs[k])
    }
  }
  if (children) {
    (Array.isArray(children) ? children : [children]).forEach((c) => node.appendChild(c))
  }
  return node
}

// Toolbar button descriptor: { id, label, title, active(editor), run(editor) }
function buttons() {
  return [
    { id: 'para', label: 'P', title: 'Paragraph', active: (e) => e.isActive('paragraph'), run: (e) => e.chain().focus().setParagraph().run() },
    { id: 'h1', label: 'H1', title: 'Heading 1', active: (e) => e.isActive('heading', { level: 1 }), run: (e) => e.chain().focus().toggleHeading({ level: 1 }).run() },
    { id: 'h2', label: 'H2', title: 'Heading 2', active: (e) => e.isActive('heading', { level: 2 }), run: (e) => e.chain().focus().toggleHeading({ level: 2 }).run() },
    { id: 'h3', label: 'H3', title: 'Heading 3', active: (e) => e.isActive('heading', { level: 3 }), run: (e) => e.chain().focus().toggleHeading({ level: 3 }).run() },
    'sep',
    { id: 'bold', label: 'B', title: 'Bold', active: (e) => e.isActive('bold'), run: (e) => e.chain().focus().toggleBold().run() },
    { id: 'italic', label: 'I', title: 'Italic', active: (e) => e.isActive('italic'), run: (e) => e.chain().focus().toggleItalic().run() },
    { id: 'underline', label: 'U', title: 'Underline', active: (e) => e.isActive('underline'), run: (e) => e.chain().focus().toggleUnderline().run() },
    { id: 'strike', label: 'S', title: 'Strikethrough', active: (e) => e.isActive('strike'), run: (e) => e.chain().focus().toggleStrike().run() },
    'sep',
    { id: 'ul', label: '•≡', title: 'Bullet list', active: (e) => e.isActive('bulletList'), run: (e) => e.chain().focus().toggleBulletList().run() },
    { id: 'ol', label: '1.', title: 'Numbered list', active: (e) => e.isActive('orderedList'), run: (e) => e.chain().focus().toggleOrderedList().run() },
    'sep',
    { id: 'quote', label: '❝', title: 'Blockquote', active: (e) => e.isActive('blockquote'), run: (e) => e.chain().focus().toggleBlockquote().run() },
    { id: 'code', label: '</>', title: 'Code block', active: (e) => e.isActive('codeBlock'), run: (e) => e.chain().focus().toggleCodeBlock().run() },
    'sep',
    { id: 'link', label: '🔗', title: 'Link', active: (e) => e.isActive('link'), run: (e) => toggleLink(e) },
    { id: 'image', label: '🖼', title: 'Insert image', active: () => false, run: (e) => insertImage(e) },
    { id: 'table', label: '⊞', title: 'Insert table', active: (e) => e.isActive('table'), run: (e) => e.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run() },
    'sep',
    { id: 'align-l', label: '⯇', title: 'Align left', active: (e) => e.isActive({ textAlign: 'left' }), run: (e) => e.chain().focus().setTextAlign('left').run() },
    { id: 'align-c', label: '⇶', title: 'Align center', active: (e) => e.isActive({ textAlign: 'center' }), run: (e) => e.chain().focus().setTextAlign('center').run() },
    { id: 'align-r', label: '⯈', title: 'Align right', active: (e) => e.isActive({ textAlign: 'right' }), run: (e) => e.chain().focus().setTextAlign('right').run() },
    'sep',
    { id: 'undo', label: '↺', title: 'Undo', active: () => false, run: (e) => e.chain().focus().undo().run() },
    { id: 'redo', label: '↻', title: 'Redo', active: () => false, run: (e) => e.chain().focus().redo().run() },
  ]
}

function toggleLink(editor) {
  const prev = editor.getAttributes('link').href
  const url = window.prompt('Link URL', prev || 'https://')
  if (url === null) return
  if (url === '' || url === 'https://') {
    editor.chain().focus().extendMarkRange('link').unsetLink().run()
    return
  }
  editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
}

function insertImage(editor) {
  const input = el('input', { type: 'file', accept: 'image/*' })
  input.style.display = 'none'
  input.addEventListener('change', () => {
    const f = input.files && input.files[0]
    if (!f) return
    uploadFile(f)
      .then((url) => editor.chain().focus().setImage({ src: url }).run())
      .catch((err) => window.alert('Image upload failed: ' + err.message))
  })
  document.body.appendChild(input)
  input.click()
  input.remove()
}

function refreshActive(refreshables, editor) {
  refreshables.forEach(({ btn, b }) => {
    btn.classList.toggle('is-active', b.active(editor))
  })
}

// Sync editor HTML into the hidden form field. `editor.isEmpty` keeps an
// untouched editor as '' so the form's `required` validation still works.
function syncSource(editor, source) {
  if (!source) return
  source.value = editor.isEmpty ? '' : editor.getHTML()
}

/**
 * Initialize a rich editor inside `root` and sync HTML into `source`.
 * Options: { root, source, initialContent, placeholder }
 * Returns the TipTap editor instance.
 */
function init(opts) {
  const root = opts.root
  const source = opts.source || null
  const initialContent = opts.initialContent || ''
  const placeholder = opts.placeholder || ''

  root.classList.add('dohw-editor')
  root.innerHTML = ''

  const toolbar = el('div', { class: 'dohw-toolbar' })
  const contentHost = el('div', { class: 'dohw-content' })

  const editor = new Editor({
    element: contentHost,
    content: initialContent,
    extensions: [
      StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
      Underline,
      Link.configure({ openOnClick: false, autolink: true }),
      Image.configure({ allowBase64: false }),
      TableKit.configure({ table: { resizable: true } }),
      TextAlign.configure({ types: ['heading', 'paragraph'] }),
      Placeholder.configure({ placeholder }),
    ],
  })

  const refreshables = []
  buttons().forEach((b) => {
    if (b === 'sep') {
      toolbar.appendChild(el('span', { class: 'dohw-sep' }))
      return
    }
    const btn = el('button', { type: 'button', class: 'dohw-btn', title: b.title, 'data-id': b.id, text: b.label })
    btn.addEventListener('mousedown', (ev) => ev.preventDefault())
    btn.addEventListener('click', () => b.run(editor))
    toolbar.appendChild(btn)
    refreshables.push({ btn, b })
  })

  root.appendChild(toolbar)
  root.appendChild(contentHost)

  editor.on('update', ({ editor }) => {
    syncSource(editor, source)
    refreshActive(refreshables, editor)
  })
  editor.on('selectionUpdate', () => refreshActive(refreshables, editor))

  syncSource(editor, source)
  refreshActive(refreshables, editor)

  return editor
}

window.DoWHEditor = { init, uploadFile }
