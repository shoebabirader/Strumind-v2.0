'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { mlApi, generativeApi } from '@/lib/api';

interface AIAssistantDialogProps {
  open: boolean;
  onClose: () => void;
}

export function AIAssistantDialog({ open, onClose }: AIAssistantDialogProps) {
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([
    { role: 'assistant', content: 'Hello! I\'m your AI structural engineering assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      // Simulate AI response (replace with actual API call)
      setTimeout(() => {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: 'I can help you with:\n• Structural analysis\n• Member design\n• Code compliance\n• Optimization suggestions\n\nWhat would you like to know?'
        }]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('AI request failed:', error);
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] h-[600px] flex flex-col">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle>AI Assistant</DialogTitle>
            <Badge variant="secondary">Beta</Badge>
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4 p-4 bg-gray-50 rounded-lg">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-200'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 p-3 rounded-lg">
                <p className="text-sm text-gray-500">Thinking...</p>
              </div>
            </div>
          )}
        </div>

        <div className="flex space-x-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask me anything about structural engineering..."
            disabled={loading}
          />
          <Button onClick={handleSend} disabled={loading || !input.trim()}>
            Send
          </Button>
        </div>

        <div className="flex flex-wrap gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => setInput('Suggest optimal beam size for 6m span')}
          >
            Suggest beam size
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => setInput('Check code compliance for my design')}
          >
            Check compliance
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => setInput('Optimize material usage')}
          >
            Optimize design
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
