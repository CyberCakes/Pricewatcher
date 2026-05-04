import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(email, password);
      setSuccess('Регистрация успешна! Теперь войдите.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
    }
  };

  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '3rem' }}>
      <div className="card">
        <h2>Регистрация</h2>
        {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
        {success && <div style={{ color: 'green', marginBottom: '1rem' }}>{success}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Пароль</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="btn btn-primary">Зарегистрироваться</button>
        </form>
        <p style={{ marginTop: '1rem' }}>Уже есть аккаунт? <Link to="/login">Войти</Link></p>
      </div>
    </div>
  );
}