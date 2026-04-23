// nie wiem czy ta strona zostanie, na stronie admina jest coś takiego jak "dodaj użytkownika"
// spełnia to funkcje rejestracje czy dodaje uzytkownika do zespolu/projektu

// rejestracja miała na celu tylko sprawdzić czy uda sie połączyć z backendem, poprawnie utworzyć użytkowniak
// i wygenerować json token do autentykacji


// jak tutaj się utworzy usera, to przekierowuje na podstrone login

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log("FORM SUBMIT DZIAŁA"); 
    try {
      const res = await fetch('http://localhost:8000/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          first_name: firstName,
          last_name: lastName,
          password,
        }),
      });

      if (res.ok) {
        navigate('/login');
      } else {
        console.log('Błąd rejestracji');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="w-full max-w-sm text-center">
        <h1 className="mb-2">ScrumBoard</h1>
        <p className="mb-8 opacity-80">Utwórz nowe konto</p>

        <div
          className="p-8 rounded-lg shadow-lg text-left"
          style={{
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--border)',
            boxShadow: 'var(--shadow)',
          }}
        >
          <form onSubmit={handleSubmit} className="space-y-4">

            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 rounded border"
            />

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 rounded border"
            />

            <input
              type="text"
              placeholder="Imię"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full px-4 py-2 rounded border"
            />

            <input
              type="text"
              placeholder="Nazwisko"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full px-4 py-2 rounded border"
            />

            <input
              type="password"
              placeholder="Hasło"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 rounded border"
            />

            <button
              type="submit"
              className="w-full py-3 rounded-lg font-bold text-white"
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