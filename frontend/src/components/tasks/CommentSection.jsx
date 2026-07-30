import { useEffect, useState } from 'react'
import * as commentsApi from '../../api/comments'
import ErrorMessage from '../common/ErrorMessage'

export default function CommentSection({ taskId }) {
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [newComment, setNewComment] = useState('')
  const [posting, setPosting] = useState(false)

  useEffect(() => {
    let cancelled = false

    async function loadComments() {
      setLoading(true)
      setError('')
      try {
        const data = await commentsApi.listTaskComments(taskId)
        if (!cancelled) setComments(data)
      } catch (err) {
        if (!cancelled) setError(err.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadComments()
    return () => {
      cancelled = true
    }
  }, [taskId])

  async function handleAddComment(e) {
    e.preventDefault()
    if (!newComment.trim()) return

    setPosting(true)
    setError('')
    try {
      const created = await commentsApi.addTaskComment(taskId, newComment.trim())
      setComments((prev) => [...prev, created])
      setNewComment('')
    } catch (err) {
      setError(err.message)
    } finally {
      setPosting(false)
    }
  }

  return (
    <div className="comment-section">
      <ErrorMessage message={error} />
      {loading ? (
        <p className="page-subtitle">Loading comments…</p>
      ) : comments.length === 0 ? (
        <p className="page-subtitle">No comments yet.</p>
      ) : (
        comments.map((c) => (
          <div className="comment" key={c.id}>
            <span className="comment-author">{c.author_name}</span>
            <span className="comment-meta">
              {new Date(c.created_at).toLocaleString()}
            </span>
            <div>{c.comment}</div>
          </div>
        ))
      )}

      <form className="comment-form" onSubmit={handleAddComment}>
        <input
          className="form-input"
          placeholder="Add a comment…"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
        />
        <button type="submit" className="btn btn-secondary btn-sm" disabled={posting}>
          {posting ? 'Posting…' : 'Post'}
        </button>
      </form>
    </div>
  )
}
