import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('programmer');

  const handleSubmit = (e) => {
    e.preventDefault();

    const userData = {
      username,
      password,
      role,
    };

    console.log('REGISTER:', userData);
    //rozrzucamy do konkretnych widoków
    if (role === 'scrum_master'){
      navigate('/scrum-master');
    } else if (role === 'product_owner') {
      navigate('/product-owner');
    } else{
      navigate('/programmer');
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
            boxShadow: 'var(--shadow)' 
          }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* USERNAME */}
            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Nazwa użytkownika
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 rounded border"
                required
              />
            </div>

            {/* PASSWORD */}
            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Hasło
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 rounded border"
                required
              />
            </div>

            {/* ROLE SELECTION */}
            <div className="space-y-2">
              <label className="block font-medium" style={{ color: 'var(--text-h)' }}>
                Wybierz rolę
              </label>

              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-4 py-2 rounded border cursor-pointer"
              >
                <option value="scrum_master">Scrum Master</option>
                <option value="product_owner">Product Owner</option>
                <option value="programmer">Programmer</option>
              </select>
            </div>

            <button
              type="submit"
              className="w-full py-3 rounded-lg font-bold text-white transition-all hover:opacity-90 cursor-pointer"
              style={{ backgroundColor: 'var(--accent)' }}
            >
              Zarejestruj się
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}