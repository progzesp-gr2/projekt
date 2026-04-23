import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
  e.preventDefault();

  // polaczenie z backendem
  //  polaczenie z baza oraz gerneracja json token
  const res = await fetch('http://localhost:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    const data = await res.json();

    if (res.ok) {
      // zapis tokenów
      localStorage.setItem('access', data.access);
      localStorage.setItem('refresh', data.refresh);

      navigate('/dashboard');
    } else {
      console.log("Błąd logowania", data);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="w-full max-w-sm text-center">
        <h1 className="mb-2">ScrumBoard</h1>
        <p className="mb-8 opacity-80">Zaloguj się do systemu</p>

        <div 
          className="p-8 rounded-lg shadow-lg text-left"
          style={{ 
            backgroundColor: 'var(--bg)', 
            border: '1px solid var(--border)',
            boxShadow: 'var(--shadow)' 
          }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            
            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Nazwa użytkownika (lub e-mail)
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 rounded border focus:outline-none transition-all"
                style={{ 
                  backgroundColor: 'var(--code-bg)', 
                  borderColor: 'var(--border)',
                  color: 'var(--text-h)'
                }}
                placeholder="admin"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Hasło
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 rounded border focus:outline-none transition-all"
                style={{ 
                  backgroundColor: 'var(--code-bg)', 
                  borderColor: 'var(--border)',
                  color: 'var(--text-h)'
                }}
                placeholder="admin"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full py-3 rounded-lg font-bold text-white transition-all hover:opacity-90"
              style={{ backgroundColor: 'var(--accent)' }}
            >
              Zaloguj się
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}