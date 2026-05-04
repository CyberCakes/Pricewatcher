import { Link, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const isAuth = !!localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">PriceWatcher</Link>
        <div className="navbar-nav">
          {isAuth ? (
            <>
              <Link to="/dashboard">Мои товары</Link>
              <button onClick={handleLogout} className="btn">Выйти</button>
            </>
          ) : (
            <>
              <Link to="/login">Вход</Link>
              <Link to="/register">Регистрация</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}