import { useState } from 'react'
import { mlAPI } from '@/lib/api'

export default function AIAssistant() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await mlAPI.predict({
        model_type: 'design_assistant',
        input_data: { query: input }
      })

      const aiMessage = {
        role: 'assistant',
        content: JSON.stringify(response.data.predictions, null, 2)
      }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('AI request failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow">
      <div className="p-4 border-b">
        <h3 className="font-bold">AI Design Assistant</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded ${
              msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8'
            }`}
          >
            <pre className="text-sm whitespace-pre-wrap">{msg.content}</pre>
          </div>
        ))}
        {loading && <div className="text-gray-500">Thinking...</div>}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask for design suggestions..."
            className="flex-1 p-2 border rounded"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  )
}
