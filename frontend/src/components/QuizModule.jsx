import React, { useState } from 'react'
import axios from 'axios'
import { Loader2, CheckCircle2, XCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const QuizModule = () => {
  const [subject, setSubject] = useState('Physics')
  const [topic, setTopic] = useState('Newton\'s Laws')
  const [quiz, setQuiz] = useState(null)
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const generateQuiz = async () => {
    if (!subject.trim() || !topic.trim()) return
    setLoading(true)
    setQuiz(null)
    setResults(null)
    setAnswers({})
    try {
      const res = await axios.post('http://localhost:8000/api/quiz/generate', { subject, topic, num_questions: 10 })
      setQuiz(res.data.quiz)
    } catch (err) {
      alert('Failed to generate quiz. Check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const submitQuiz = async () => {
    if (Object.keys(answers).length < quiz.length) {
      alert('Please answer all questions first!')
      return
    }
    setLoading(true)
    try {
      const res = await axios.post('http://localhost:8000/api/quiz/evaluate', {
        subject,
        questions: quiz,
        answers
      })
      setResults(res.data)
    } catch (err) {
      alert('Failed to evaluate quiz.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full glass-panel rounded-2xl overflow-hidden relative">
      <div className="p-6 border-b border-slate-700/50 bg-surface/50 z-10 flex flex-col gap-4">
        <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-secondary to-primary">Quiz Generator</h2>
        
        <div className="flex gap-4 flex-wrap">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm text-slate-400 mb-1">Subject</label>
            <input 
              type="text" 
              value={subject} 
              onChange={e => setSubject(e.target.value)}
              className="w-full bg-slate-800/80 border border-slate-600 rounded-xl px-4 py-2 focus:outline-none focus:border-secondary transition-colors"
              placeholder="e.g. Biology"
            />
          </div>
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm text-slate-400 mb-1">Topic</label>
            <input 
              type="text" 
              value={topic} 
              onChange={e => setTopic(e.target.value)}
              className="w-full bg-slate-800/80 border border-slate-600 rounded-xl px-4 py-2 focus:outline-none focus:border-secondary transition-colors"
              placeholder="e.g. Cellular Respiration"
            />
          </div>
          <div className="flex items-end">
            <button 
              onClick={generateQuiz}
              disabled={loading || !subject.trim() || !topic.trim()}
              className="bg-secondary hover:bg-violet-600 disabled:opacity-50 text-white rounded-xl px-6 py-2 flex items-center justify-center transition-colors shadow-lg shadow-secondary/20 h-[42px]"
            >
              {loading && !quiz && !results ? <Loader2 className="animate-spin mr-2" size={18} /> : null}
              Generate Quiz
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 z-10">
        {!quiz && !loading && !results && (
          <div className="h-full flex items-center justify-center text-slate-500">
            <p>Enter a subject and topic to generate a quiz.</p>
          </div>
        )}

        {loading && !quiz && !results && (
           <div className="h-full flex flex-col items-center justify-center text-secondary gap-4">
             <Loader2 className="animate-spin" size={40} />
             <p className="animate-pulse">Generating your personalized quiz...</p>
           </div>
        )}

        <AnimatePresence mode="wait">
          {quiz && !results && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }} 
              animate={{ opacity: 1, y: 0 }} 
              exit={{ opacity: 0, y: -20 }}
              className="space-y-8 pb-20"
            >
              {quiz.map((q, i) => (
                <div key={i} className="bg-surface/50 border border-slate-700/50 p-6 rounded-2xl">
                  <h3 className="text-lg font-medium mb-4 flex items-center justify-between">
                    <div>
                      <span className="text-secondary font-bold mr-2">Q{i + 1}.</span> 
                      {q.question}
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full border ${q.complexity === 'Hard' ? 'bg-red-500/20 text-red-400 border-red-500/50' : q.complexity === 'Medium' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50' : 'bg-green-500/20 text-green-400 border-green-500/50'}`}>
                      {q.complexity}
                    </span>
                  </h3>
                  <div className="space-y-2">
                    {q.options.map((opt, optIdx) => (
                      <label 
                        key={optIdx} 
                        className={`flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-all ${
                          answers[i] === optIdx 
                            ? 'bg-secondary/20 border-secondary text-white' 
                            : 'border-slate-700 hover:border-slate-500 text-slate-300 hover:bg-white/5'
                        }`}
                      >
                        <input 
                          type="radio" 
                          name={`q-${i}`} 
                          className="hidden"
                          checked={answers[i] === optIdx}
                          onChange={() => setAnswers({...answers, [i]: optIdx})}
                        />
                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${answers[i] === optIdx ? 'border-secondary' : 'border-slate-500'}`}>
                          {answers[i] === optIdx && <div className="w-2.5 h-2.5 rounded-full bg-secondary" />}
                        </div>
                        {opt}
                      </label>
                    ))}
                  </div>
                </div>
              ))}
              
              <div className="flex justify-center mt-8">
                <button 
                  onClick={submitQuiz}
                  disabled={loading}
                  className="bg-primary hover:bg-blue-600 text-white rounded-xl px-10 py-3 font-medium transition-all shadow-lg shadow-primary/20 hover:-translate-y-1"
                >
                  {loading ? <Loader2 className="animate-spin inline mr-2" size={20} /> : null}
                  Submit Answers
                </button>
              </div>
            </motion.div>
          )}

          {results && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }} 
              animate={{ opacity: 1, scale: 1 }} 
              className="space-y-6"
            >
              <div className="bg-surface border border-slate-700/50 p-8 rounded-2xl text-center">
                <h3 className="text-4xl font-bold mb-2 text-white">Score: {results.score} / {results.total}</h3>
                <div className="inline-block px-4 py-1 rounded-full bg-slate-800 text-slate-300 text-sm mb-6 border border-slate-700">
                  {Math.round((results.score / results.total) * 100)}% Accuracy
                </div>
                
                <div className="bg-slate-800/50 rounded-xl p-6 text-left border border-slate-700/50">
                  <h4 className="font-bold text-accent mb-2 flex items-center gap-2">🤖 AI Feedback</h4>
                  <p className="text-slate-300 leading-relaxed">{results.feedback}</p>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="text-xl font-bold">Review Answers</h4>
                {results.results.map((res, i) => (
                  <div key={i} className={`p-5 rounded-xl border ${res.is_correct ? 'border-green-500/30 bg-green-500/5' : 'border-red-500/30 bg-red-500/5'}`}>
                    <h5 className="font-medium mb-3 flex gap-2 items-start">
                      {res.is_correct ? <CheckCircle2 className="text-green-500 shrink-0" /> : <XCircle className="text-red-500 shrink-0" />}
                      <span>{res.question}</span>
                    </h5>
                    {!res.is_correct && (
                      <p className="text-sm text-red-400 ml-8 mb-1">Your answer: {quiz[i].options[res.student_answer]}</p>
                    )}
                    <p className={`text-sm ml-8 mb-2 ${res.is_correct ? 'text-green-400' : 'text-slate-300'}`}>
                      Correct answer: {res.correct_option}
                    </p>
                    <div className="ml-8 mt-2 p-3 bg-slate-800/80 rounded border border-slate-700/50">
                      <span className="text-xs text-accent font-bold mb-1 block">💡 Explanation</span>
                      <p className="text-sm text-slate-300">{res.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default QuizModule
