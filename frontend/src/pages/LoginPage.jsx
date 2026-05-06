import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const { data } = await client.post('/api/auth/login', { username, password });

      switch (data.role) {
        case 'PRODUCT_OWNER':
          navigate('/product-owner');
          break;
        case 'SCRUM_MASTER':
          navigate('/scrum-master');
          break;
        case 'PROGRAMMER':
          navigate('/programmer');
          break;
        default:
          navigate('/login');
      }
    } catch (err) {
        const data = err.response?.data;
        if (data?.non_field_errors) {
          setError(data.non_field_errors[0]);
        } else {
          setError('Błąd logowania');
    }
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
            boxShadow: 'var(--shadow)',
          }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">

            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Nazwa użytkownika
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 rounded border focus:outline-none transition-all"
                style={{
                  backgroundColor: 'var(--code-bg)',
                  borderColor: 'var(--border)',
                  color: 'var(--text-h)',
                }}
                placeholder="username"
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
                  color: 'var(--text-h)',
                }}
                placeholder="hasło"
                required
              />
            </div>

            {error && (
              <p className="text-sm text-red-500">
                {typeof error === 'string' ? error : JSON.stringify(error)}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-lg font-bold text-white transition-all hover:opacity-90 cursor-pointer disabled:opacity-50"
              style={{ backgroundColor: 'var(--accent)' }}
            >
              {loading ? 'Logowanie...' : 'Zaloguj się'}
            </button>

            <p className="text-center mt-4 text-sm opacity-80">
              Nie masz konta?{' '}
              <span
                onClick={() => navigate('/register')}
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