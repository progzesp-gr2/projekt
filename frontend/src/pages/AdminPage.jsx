import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AdminPage() {
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState('users');

  const stats = [
    { label: 'Liczba użytkowników', value: '1', color: '#aa3bff' },
    { label: 'Projekty', value: '3', color: '#3b82f6' },
    { label: 'Wszystkie zadania', value: '1', color: '#10b981' },
    { label: 'Ukończone', value: '0', percentage: '0%', color: '#10b981' },
  ];

  const [users, setUsers] = useState([
    { id: 'AA', name: 'Admin Admin', email: 'admin@admin.pl', role: 'Administrator', tasks: 1 },
  ]);

  return (
    <div className="flex-1 flex flex-col p-8 text-left bg-gray-50/30">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h2 className="m-0 text-2xl font-bold" style={{ color: 'var(--text-h)' }}>Panel Administracyjny</h2>
          <p className="text-sm opacity-60">Zarządzanie systemem Scrum</p>
        </div>
        <button 
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-md border text-sm font-medium hover:bg-gray-100 transition-all"
          style={{ borderColor: 'var(--border)', backgroundColor: 'var(--bg)' }}
        >
          Wyloguj
        </button>
      </header>

      {/* statystyki */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {stats.map((stat, i) => (
          <div 
            key={i} 
            className="p-6 rounded-xl border flex justify-between items-start"
            style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)', boxShadow: 'var(--shadow)' }}
          >
            <div>
              <p className="text-xs font-semibold uppercase opacity-50 mb-1">{stat.label}</p>
              <h1 className="m-0 text-3xl font-black">{stat.value}</h1>
            </div>
            <span className="text-sm font-bold text-green-500">{stat.percentage}</span>
          </div>
        ))}
      </div>

      {/* nawigacja zakładek */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex gap-2 p-1 rounded-lg bg-gray-100 border" style={{ borderColor: 'var(--border)' }}>
          {['users', 'projects', 'settings'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all ${
                activeTab === tab ? 'bg-white shadow-sm opacity-100' : 'opacity-60 hover:opacity-100'
              }`}
            >
              {tab === 'users' && 'Użytkownicy'}
              {tab === 'projects' && 'Projekty'}
              {tab === 'settings' && 'Ustawienia'}
            </button>
          ))}
        </div>
        
        {activeTab === 'users' && (
          <button 
            className="px-6 py-2 rounded-lg text-white font-bold text-sm transition-all hover:scale-[1.02]"
            style={{ backgroundColor: 'var(--accent)' }}
          >
            + Dodaj użytkownika
          </button>
        )}
      </div>

      {/* content zakładki*/}
      <div 
        className="rounded-xl border overflow-hidden min-h-[300px] flex flex-col" 
        style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)', boxShadow: 'var(--shadow)' }}
      >
        {activeTab === 'users' ? (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b" style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}>
                <th className="p-4 text-xs uppercase opacity-60">Użytkownik</th>
                <th className="p-4 text-xs uppercase opacity-60">Email</th>
                <th className="p-4 text-xs uppercase opacity-60">Rola</th>
                <th className="p-4 text-xs uppercase opacity-60">Liczba zadań</th>
                <th className="p-4 text-xs uppercase opacity-60 text-right">Akcje</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, idx) => (
                <tr key={idx} className="border-b last:border-0 hover:bg-gray-50/50 transition-colors" style={{ borderColor: 'var(--border)' }}>
                  <td className="p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-xs" style={{ backgroundColor: 'var(--accent)' }}>
                      {user.id}
                    </div>
                    <span className="font-medium" style={{ color: 'var(--text-h)' }}>{user.name}</span>
                  </td>
                  <td className="p-4 text-sm opacity-80">{user.email}</td>
                  <td className="p-4">
                    <span className="px-3 py-1 rounded-full text-[10px] font-bold bg-gray-100 border">
                      {user.role}
                    </span>
                  </td>
                  <td className="p-4 text-sm font-medium">{user.tasks}</td>
                  <td className="p-4 text-right">
                    <button className="mr-3 opacity-40 hover:opacity-100">Edytuj</button>
                    <button className="opacity-40 hover:opacity-100 text-red-500">Usuń</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          /* placeholder */
          <div className="flex-1 flex flex-col items-center justify-center p-20 text-center">
            <h2 className="mb-2">Wkrótce</h2>
          </div>
        )}
      </div>
    </div>
  );
}