import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, Save, Loader2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'

const ChatModule = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [subject, setSubject] = useState('Computer Science')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || !subject.trim()) return

    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg, { role: 'assistant', content: '', mood: 'neutral' }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject,
          message: userMsg.content,
          context: ''
        })
      })

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let done = false

      setLoading(false)

      while (!done) {
        const { value, done: doneReading } = await reader.read()
        done = doneReading
        if (value) {
          const chunkStr = decoder.decode(value, { stream: true })
          const lines = chunkStr.split('\n')
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                setMessages(prev => {
                  const newMsgs = [...prev]
                  const lastMsg = newMsgs[newMsgs.length - 1]
                  if (lastMsg && lastMsg.role === 'assistant') {
                    if (data.mood) lastMsg.mood = data.mood
                    if (data.chunk) lastMsg.content += data.chunk
                  }
                  return newMsgs
                })
              } catch (e) {
                console.error("Error parsing stream data", e, line)
              }
            }
          }
        }
      }
    } catch (err) {
      setMessages(prev => {
        const newMsgs = [...prev]
        const lastMsg = newMsgs[newMsgs.length - 1]
        if (lastMsg && lastMsg.role === 'assistant') {
          lastMsg.content = 'Sorry, there was an error processing your request.'
        }
        return newMsgs
      })
      setLoading(false)
    }
  }

  const saveNote = async (content) => {
    try {
      await axios.post('http://localhost:8000/api/notes', { content })
      alert('Note saved successfully!')
    } catch (err) {
      alert('Failed to save note.')
    }
  }

  const getMoodColor = (mood) => {
    switch (mood) {
      case 'happy': return 'bg-green-500/20 text-green-400 border-green-500/50'
      case 'frustrated': return 'bg-red-500/20 text-red-400 border-red-500/50'
      case 'disengaged': return 'bg-gray-500/20 text-gray-400 border-gray-500/50'
      default: return 'bg-blue-500/20 text-blue-400 border-blue-500/50'
    }
  }

  return (
    <div className="flex flex-col h-full glass-panel rounded-2xl overflow-hidden relative">
      <div className="p-4 border-b border-slate-700/50 bg-surface/50 flex items-center justify-between z-10">
        <h2 className="text-xl font-bold">Study Chat</h2>
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-400">Subject:</span>
          <input 
            type="text" 
            value={subject} 
            onChange={e => setSubject(e.target.value)}
            className="bg-slate-800/50 border border-slate-600 rounded px-3 py-1 text-sm focus:outline-none focus:border-primary w-40 transition-colors"
            placeholder="e.g. History"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 z-10">
        {messages.length === 0 && (
          <div className="h-full flex items-center justify-center text-slate-500 flex-col gap-2">
            <span className="text-4xl">👋</span>
            <p>Start chatting with your AI Tutor!</p>
          </div>
        )}
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={i}
              className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'ml-auto items-end' : 'mr-auto items-start'}`}
            >
              <div className={`p-4 rounded-2xl break-words overflow-hidden ${msg.role === 'user' ? 'bg-primary text-white rounded-br-sm' : 'bg-surface border border-slate-700/50 rounded-bl-sm'}`}>
                <div className="prose prose-invert prose-slate max-w-none text-sm md:text-base">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
              {msg.role === 'assistant' && (
                <div className="flex items-center gap-2 mt-2">
                  <span className={`text-xs px-2 py-1 rounded-full border ${getMoodColor(msg.mood)} capitalize`}>
                    {msg.mood}
                  </span>
                  <button onClick={() => saveNote(msg.content)} className="text-slate-400 hover:text-white transition-colors flex items-center gap-1 text-xs">
                    <Save size={12} /> Save Note
                  </button>
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        {loading && (
          <div className="mr-auto bg-surface border border-slate-700/50 p-4 rounded-2xl rounded-bl-sm">
            <Loader2 className="animate-spin text-primary" size={20} />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-slate-700/50 bg-surface/50 z-10">
        <form onSubmit={e => { e.preventDefault(); handleSend() }} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 bg-slate-800/80 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:border-primary transition-colors text-white"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="bg-primary hover:bg-blue-600 disabled:opacity-50 text-white rounded-xl px-6 flex items-center justify-center transition-colors shadow-lg shadow-primary/20"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatModule
