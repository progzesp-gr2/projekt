import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // roboczo, do testu
  const handleSubmit = (e) => {
    e.preventDefault();

    if (username === 'admin' && password === 'admin') {
      navigate('/product-owner');
    }

    if (username === 'sm' && password === 'sm') {
      navigate('/scrum-master');
    }

    if (username === 'programmer' && password === 'programmer') {
      navigate('/programmer');
    }
  };

  // przerzucanie do panelu rejestracji
  const handleRegisterRedirect = () => {
    navigate('/register');
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
              className="w-full py-3 rounded-lg font-bold text-white transition-all hover:opacity-90 cursor-pointer"
              style={{ backgroundColor: 'var(--accent)' }}
            >
              Zaloguj się
            </button>
            {/* przycisk rejestracji */}
            <p className="text-center mt-4 text-sm opacity-80">
              Nie masz konta?{' '}
              <span
                onClick={handleRegisterRedirect}
                className="cursor-pointer underline"
                style={{ color: 'var(--accent)' }}
              >
                Zarejestruj się
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}