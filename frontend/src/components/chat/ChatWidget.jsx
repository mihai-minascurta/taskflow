import { useEffect, useRef, useState } from 'react'
import { sendChatMessage } from '../../api/chat'

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const previousResponseId = useRef(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen, loading])

  async function handleSend(event) {
    event.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    setMessages((prev) => [...prev, { role: 'user', text }])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const data = await sendChatMessage(text, previousResponseId.current)
      previousResponseId.current = data.response_id || null
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-widget">
      {isOpen && (
        <div className="chat-panel card">
          <div className="chat-panel-header">
            <span>TaskFlow Assistant</span>
            <button
              type="button"
              className="chat-close-btn"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className="chat-messages">
            {messages.length === 0 && !loading && (
              <p className="chat-empty">Ask me anything about your projects and tasks.</p>
            )}
            {messages.map((message, index) => (
              <div key={index} className={`chat-message chat-message-${message.role}`}>
                {message.text}
              </div>
            ))}
            {loading && (
              <div className="chat-message chat-message-assistant chat-message-loading">
                <span className="spinner" />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && <div className="error-box chat-error">{error}</div>}

          <form className="chat-input-row" onSubmit={handleSend}>
            <input
              type="text"
              className="form-input"
              placeholder="Type a message..."
              value={input}
              onChange={(event) => setInput(event.target.value)}
              disabled={loading}
            />
            <button
              type="submit"
              className="btn btn-primary btn-sm"
              disabled={loading || !input.trim()}
            >
              Send
            </button>
          </form>
        </div>
      )}

      <button
        type="button"
        className="chat-toggle-btn"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? '×' : '💬'}
      </button>
    </div>
  )
}
