import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Loader2, RefreshCw } from 'lucide-react'
import { motion } from 'framer-motion'

const NotesModule = () => {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchNotes = async () => {
    setLoading(true)
    try {
      const res = await axios.get('http://localhost:8000/api/notes')
      setNotes(res.data.notes || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchNotes()
  }, [])

  return (
    <div className="flex flex-col h-full glass-panel rounded-2xl overflow-hidden relative">
      <div className="p-6 border-b border-slate-700/50 bg-surface/50 z-10 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-accent to-emerald-300">My Notes</h2>
        <button 
          onClick={fetchNotes} 
          disabled={loading}
          className="text-slate-400 hover:text-white transition-colors"
        >
          <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 z-10 space-y-4">
        {loading && notes.length === 0 && (
          <div className="flex justify-center items-center h-full">
            <Loader2 className="animate-spin text-accent" size={30} />
          </div>
        )}

        {!loading && notes.length === 0 && (
          <div className="flex justify-center items-center h-full text-slate-500">
            <p>No notes saved yet. Save them from the Study Chat!</p>
          </div>
        )}

        {notes.map((note, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            key={i} 
            className="bg-surface/60 border border-slate-700/50 p-5 rounded-xl hover:bg-surface/80 transition-colors shadow-sm"
          >
            <p className="text-slate-200 whitespace-pre-wrap">{note}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default NotesModule
