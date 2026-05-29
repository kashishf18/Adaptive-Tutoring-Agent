import { useState } from 'react'
import { MessageSquare, HelpCircle, BookOpen } from 'lucide-react'
import ChatModule from './components/ChatModule'
import QuizModule from './components/QuizModule'
import NotesModule from './components/NotesModule'

function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="min-h-screen bg-background flex flex-col md:flex-row">
      {/* Sidebar Navigation */}
      <aside className="w-full md:w-64 glass-panel border-r border-slate-700/50 p-6 flex flex-col z-10 relative">
        <div className="mb-8 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white font-bold shadow-lg shadow-primary/30">
            ATA
          </div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-100 to-slate-400">
            Adaptive Tutor
          </h1>
        </div>

        <nav className="flex md:flex-col gap-2 overflow-x-auto md:overflow-visible">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all whitespace-nowrap ${
              activeTab === 'chat'
                ? 'bg-primary/20 text-primary font-medium border border-primary/20 shadow-[0_0_15px_rgba(59,130,246,0.15)]'
                : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
            }`}
          >
            <MessageSquare size={20} className={activeTab === 'chat' ? 'text-primary' : ''} />
            <span>Study Chat</span>
          </button>
          <button
            onClick={() => setActiveTab('quiz')}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all whitespace-nowrap ${
              activeTab === 'quiz'
                ? 'bg-secondary/20 text-secondary font-medium border border-secondary/20 shadow-[0_0_15px_rgba(139,92,246,0.15)]'
                : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
            }`}
          >
            <HelpCircle size={20} className={activeTab === 'quiz' ? 'text-secondary' : ''} />
            <span>Quiz Generator</span>
          </button>
          <button
            onClick={() => setActiveTab('notes')}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all whitespace-nowrap ${
              activeTab === 'notes'
                ? 'bg-accent/20 text-accent font-medium border border-accent/20 shadow-[0_0_15px_rgba(16,185,129,0.15)]'
                : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
            }`}
          >
            <BookOpen size={20} className={activeTab === 'notes' ? 'text-accent' : ''} />
            <span>My Notes</span>
          </button>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 relative overflow-hidden flex flex-col">
        {/* Background Decorative Gradients */}
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-primary/10 blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-secondary/10 blur-[120px] pointer-events-none" />
        
        <div className="flex-1 overflow-y-auto p-4 md:p-8 relative z-10">
          <div className="max-w-4xl mx-auto w-full h-full">
            {activeTab === 'chat' && <ChatModule />}
            {activeTab === 'quiz' && <QuizModule />}
            {activeTab === 'notes' && <NotesModule />}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
