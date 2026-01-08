import { useState, useEffect, useRef } from 'react'

const API_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : "http://localhost:8000/api";

function App() {
  const [view, setView] = useState('landing'); // landing, admin, user
  const [shapes, setShapes] = useState([]);
  const [form, setForm] = useState({ name: '', shape: 'circle', color: 'red' });
  const [loading, setLoading] = useState(false);
  const eventSourceRef = useRef(null);

  useEffect(() => {
    if (view !== 'landing') {
      fetchShapes();
      setupSSE();
    }
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [view]);

  const fetchShapes = async () => {
    try {
      const res = await fetch(`${API_URL}/shapes`);
      const data = await res.json();
      setShapes(data);
    } catch (error) {
      console.error(error);
    }
  };

  const setupSSE = () => {
    if (eventSourceRef.current) eventSourceRef.current.close();

    const evtSource = new EventSource(`${API_URL}/events/stream`);
    eventSourceRef.current = evtSource;

    evtSource.addEventListener("shapes", (event) => {
      const payload = JSON.parse(event.data);
      const { type, data } = payload;

      setShapes(prev => {
        if (type === 'created') {
          if (prev.find(s => s.id === data.id)) return prev;
          return [...prev, data];
        } else if (type === 'updated') {
          return prev.map(s => s.id === data.id ? data : s);
        } else if (type === 'deleted') {
          return prev.filter(s => s.id !== data.id);
        }
        return prev;
      });
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/shapes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (res.ok) {
        setForm({ ...form, name: '' });
      } else {
        alert("Error creating shape");
      }
    } catch (err) {
      alert("Failed to connect");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`${API_URL}/shapes/${id}`, { method: 'DELETE' });
    } catch (err) {
      alert("Failed to delete");
    }
  }

  // Visual Components
  const ShapeIcon = ({ type, color }) => {
    let hexColor = color;
    if (color === 'red') hexColor = '#ff4757';
    if (color === 'green') hexColor = '#2ed573';
    if (color === 'blue') hexColor = '#3742fa';
    if (color === 'yellow') hexColor = '#ffa502';
    if (color === 'black') hexColor = '#2f3542';

    const style = { backgroundColor: hexColor };

    if (type === 'triangle') {
      style.backgroundColor = 'transparent';
      style.borderBottomColor = hexColor;
      style.color = hexColor;
    }

    return <div className={`shape-icon ${type}`} style={style}></div>;
  };

  // Landing Page
  if (view === 'landing') {
    return (
      <div className="container" style={{ textAlign: 'center', marginTop: '5rem' }}>
        <h1>Select Portal</h1>
        <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center', marginTop: '2rem' }}>
          <div className="card" style={{ cursor: 'pointer', minWidth: '200px' }} onClick={() => setView('admin')}>
            <h2>👨‍💻 Admin</h2>
            <p>Manage Shapes</p>
          </div>
          <div className="card" style={{ cursor: 'pointer', minWidth: '200px' }} onClick={() => setView('user')}>
            <h2>👀 User</h2>
            <p>View Only</p>
          </div>
        </div>
      </div>
    );
  }

  // Main App
  return (
    <div className="container">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>{view === 'admin' ? 'Admin Portal' : 'User Portal'}</h1>
        <button onClick={() => setView('landing')} style={{ background: '#333' }}>Switch Portal</button>
      </header>

      <div className="grid">
        {/* Only show Create Form if Admin */}
        {view === 'admin' && (
          <div className="card">
            <h2>Create Shape</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  value={form.name}
                  onChange={e => setForm({ ...form, name: e.target.value })}
                  required
                  maxLength={100}
                />
              </div>

              <div className="form-group">
                <label>Shape</label>
                <select value={form.shape} onChange={e => setForm({ ...form, shape: e.target.value })}>
                  <option value="circle">Circle</option>
                  <option value="square">Square</option>
                  <option value="triangle">Triangle</option>
                </select>
              </div>

              <div className="form-group">
                <label>Color</label>
                <select value={form.color} onChange={e => setForm({ ...form, color: e.target.value })}>
                  <option value="red">Red</option>
                  <option value="green">Green</option>
                  <option value="blue">Blue</option>
                  <option value="yellow">Yellow</option>
                  <option value="black">Black</option>
                </select>
              </div>

              <button type="submit" disabled={loading}>
                {loading ? "Creating..." : "Create Shape"}
              </button>
            </form>
          </div>
        )}

        {/* Shape List - Full width if User */}
        <div className="card" style={view === 'user' ? { gridColumn: '1 / -1' } : {}}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Live Shapes ({shapes.length})</h2>
          </div>

          <div className="shape-list">
            {shapes.length === 0 ? (
              <div className="empty-state">No shapes yet.</div>
            ) : (
              shapes.map(item => (
                <div key={item.id} className={`shape-item ${item.color}`}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <ShapeIcon type={item.shape} color={item.color} />
                    <div>
                      <div style={{ fontWeight: 'bold' }}>{item.name}</div>
                      <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>
                        {new Date(item.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                  {/* Only show Delete if Admin */}
                  {view === 'admin' && (
                    <button className="delete-btn" onClick={() => handleDelete(item.id)}>Delete</button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
