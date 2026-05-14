/**
 * Tutaj product owner przegląda co dzieje się w danym projekcie:
 * - Tworzy zadania i nadaje im priorytet
 * - sprawdza backlog projektu
 * - tutaj są statystyki projektu
 * - można patrzyć kto jest w projekcie 
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import BacklogTab from '../components/BacklogTab';
import { useParams } from 'react-router-dom';



export default function ProjectDashboardPage() {
  const navigate = useNavigate();
  const { id } = useParams(); //żeby było wiadomo na jakim projekcie pracujemy
  console.log(id);

  const [activeTab, setActiveTab] = useState('backlog');

  const stats = [
    { label: 'Liczba członków', value: '1', color: '#aa3bff' },
    { label: 'Projekty', value: '3', color: '#3b82f6' },
    { label: 'Wszystkie zadania', value: '1', color: '#10b981' },
    { label: 'Ukończone', value: '0', percentage: '0%', color: '#10b981' },
  ];

  const [members] = useState([
    {
      id: 'P1',
      name: 'Jan Kowalski',
      email: 'jan@example.com',
      role: 'programista',
      tasks: 5,
    },
    {
      id: 'P2',
      name: 'Anna Nowak',
      email: 'anna@example.com',
      role: 'programista',
      tasks: 3,
    },
    {
    id: 'SM1',
    name: 'Michał Scrum',
    email: 'scrum@example.com',
    role: 'scrum master',
    tasks: 1,
  },
  {
    id: 'PO1',
    name: 'Katarzyna Product',
    email: 'po@example.com',
    role: 'product owner',
    tasks: 2,
  },
  ]);

  

  const getRoleStyle = (role) => {
    switch (role?.toLowerCase()) {
      case 'administrator':
        return 'bg-red-100 text-red-700 border-red-200';
      case 'product owner':
        return 'bg-purple-100 text-purple-700 border-purple-200';
      case 'scrum master':
        return 'bg-orange-100 text-orange-700 border-orange-200';
      case 'programista':
        return 'bg-blue-100 text-blue-700 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-600 border-gray-200'; 
    }
  };

  return (
    <div className="flex-1 flex flex-col p-8 text-left bg-gray-50/30">
      <header className="flex justify-between items-center mb-10">
      <div>
        <h2
          className="m-0 text-2xl font-bold"
          style={{ color: 'var(--text-h)' }}
        >
          Panel Administracyjny
        </h2>

        <p className="text-sm opacity-60">
          Zarządzanie systemem Scrum
        </p>
      </div>

      {/* RIGHT SIDE */}
      <div className="flex items-center gap-3">

        <button
          onClick={() => navigate('/product-owner')}
          className="px-4 py-2 rounded-md border text-sm font-medium hover:bg-gray-100 transition-all cursor-pointer"
          style={{
            borderColor: 'var(--border)',
            backgroundColor: 'var(--bg)',
          }}
        >
          ← Projekty
        </button>

        <button
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-md border text-sm font-medium hover:bg-gray-100 transition-all cursor-pointer"
          style={{
            borderColor: 'var(--border)',
            backgroundColor: 'var(--bg)',
          }}
        >
          Wyloguj
        </button>

      </div>

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
        <div
          className="flex gap-2 p-1 rounded-lg border"
          style={{ backgroundColor: 'var(--code-bg)', borderColor: 'var(--border)' }}
        >
          {['backlog', 'members'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all cursor-pointer ${
                activeTab === tab ? 'shadow-sm opacity-100' : 'opacity-60 hover:opacity-100'
              }`}
              style={{
                backgroundColor: activeTab === tab ? 'var(--bg)' : 'transparent',
                color: activeTab === tab ? 'var(--text-h)' : 'inherit'
              }}
            >
              {tab === 'backlog' ? 'Backlog' : 'Członkowie'}
              
              
            </button>
          ))}
        </div>
      </div>

      {/* content zakładki*/}
      <div 
        className="rounded-xl border overflow-hidden min-h-[300px] flex flex-col" 
        style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)', boxShadow: 'var(--shadow)' }}
      >
        {activeTab === 'members' ? (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b" style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}>
                <th className="p-4 text-xs uppercase opacity-60">Członek</th>
                <th className="p-4 text-xs uppercase opacity-60">Email</th>
                <th className="p-4 text-xs uppercase opacity-60">Rola</th>
                <th className="p-4 text-xs uppercase opacity-60">Liczba zadań</th>
                <th className="p-4 text-xs uppercase opacity-60 text-right">Akcje</th>
              </tr>
            </thead>
            <tbody>
              {members.map((user, idx) => (
                <tr key={idx} className="border-b last:border-0 hover:bg-gray-50/50 transition-colors" style={{ borderColor: 'var(--border)' }}>
                  <td className="p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-xs" style={{ backgroundColor: 'var(--accent)' }}>
                      {user.id}
                    </div>
                    <span className="font-medium" style={{ color: 'var(--text-h)' }}>{user.name}</span>
                  </td>
                  <td className="p-4 text-sm opacity-80">{user.email}</td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-[10px] font-bold border ${getRoleStyle(user.role)}`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="p-4 text-sm font-medium">{user.tasks}</td>
                  <td className="p-4 text-right">
                    <button className="mr-3 opacity-40 hover:opacity-100 cursor-pointer">Edytuj</button>
                    <button className="opacity-40 hover:opacity-100 text-red-500 cursor-pointer">Usuń</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
            
          ) : activeTab === 'backlog' ? (
            <BacklogTab projectId={id} />
            //GET /api/projects/:id/backlog
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-20 text-center">
            <h2 className="mb-2">Wkrótce</h2>
            </div>
          )}

        {/* tutaj koniec */}
      </div>
    </div>
  );
}