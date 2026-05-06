import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('PROGRAMMER');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await client.post('/api/auth/register', { username, password, role });
      navigate('/login');
    } catch (err) {
      setError(err.response?.data || 'Błąd rejestracji');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="w-full max-w-sm text-center">
        <h1 className="mb-2">ScrumBoard</h1>
        <p className="mb-8 opacity-80">Zarejestruj się</p>

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
                className="w-full px-4 py-2 rounded border"
                style={{ backgroundColor: 'var(--code-bg)', borderColor: 'var(--border)' }}
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
                className="w-full px-4 py-2 rounded border"
                style={{ backgroundColor: 'var(--code-bg)', borderColor: 'var(--border)' }}
                required
              />
            </div>

            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Wybierz rolę
              </label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-4 py-2 rounded border cursor-pointer"
                style={{ backgroundColor: 'var(--code-bg)', borderColor: 'var(--border)' }}
              >
                <option value="SCRUM_MASTER">Scrum Master</option>
                <option value="PRODUCT_OWNER">Product Owner</option>
                <option value="PROGRAMMER">Programmer</option>
              </select>
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
              {loading ? 'Rejestrowanie...' : 'Zarejestruj się'}
            </button>

            <p className="text-center mt-4 text-sm opacity-80">
              Masz już konto?{' '}
              <span
                onClick={() => navigate('/login')}
                className="cursor-pointer underline"
                style={{ color: 'var(--accent)' }}
              >
                Zaloguj się
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}