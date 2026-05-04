import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login } from '../api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await login(email, password);
      localStorage.setItem('access_token', res.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError('Неверный email или пароль');
    }
  };

  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '3rem' }}>
      <div className="card">
        <h2>Вход</h2>
        {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Пароль</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="btn btn-primary">Войти</button>
        </form>
        <p style={{ marginTop: '1rem' }}>Нет аккаунта? <Link to="/register">Зарегистрироваться</Link></p>
      </div>
    </div>
  );
}