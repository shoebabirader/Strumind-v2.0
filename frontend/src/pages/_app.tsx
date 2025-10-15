import '@/styles/globals.css'
import '@/styles/professional.css'
import type { AppProps } from 'next/app'
import { AuthProvider } from '@/contexts/AuthContext'
import { ModelProvider } from '@/contexts/ModelContext'
import { SelectionProvider } from '@/contexts/SelectionContext'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <ModelProvider>
        <SelectionProvider>
          <Component {...pageProps} />
        </SelectionProvider>
      </ModelProvider>
    </AuthProvider>
  )
}
