import React from 'react'
import { useRouter } from 'next/router'
import { Zap, Shield, Sparkles, BarChart3 } from 'lucide-react'

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-4">
            Stru<span className="text-blue-400">Mind</span>
          </h1>
          <p className="text-2xl text-gray-300 mb-8">
            AI-Powered Structural Engineering Platform
          </p>
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => router.push('/register')}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-semibold"
            >
              Get Started
            </button>
            <button
              onClick={() => router.push('/login')}
              className="px-8 py-3 border-2 border-blue-400 text-blue-400 rounded-lg hover:bg-blue-400 hover:text-white text-lg font-semibold"
            >
              Login
            </button>
            <button
              onClick={() => router.push('/workspace')}
              className="px-8 py-3 border-2 border-white text-white rounded-lg hover:bg-white hover:text-gray-900 text-lg font-semibold"
            >
              View Demo
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {[
            { icon: Zap, title: 'Fast Analysis', desc: '8x faster with parallel execution' },
            { icon: Shield, title: 'Enterprise Security', desc: 'JWT auth & RBAC' },
            { icon: Sparkles, title: 'AI-Powered', desc: 'Generative design & optimization' },
            { icon: BarChart3, title: 'Real-time Collab', desc: 'WebSocket collaboration' },
          ].map((feature, idx) => (
            <div key={idx} className="bg-white bg-opacity-10 backdrop-blur-lg rounded-lg p-6 text-center">
              <feature.icon className="w-12 h-12 mx-auto mb-4 text-blue-400" />
              <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
              <p className="text-gray-300">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
