import Button from 'react-bootstrap/Button';
import { FaGithub } from 'react-icons/fa';

interface NavBarProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
  onLogin: () => void;
  onToggleSidebar: () => void;
}

export default function NavBar({
  darkMode,
  toggleDarkMode,
  onLogin,
  onToggleSidebar,
}: NavBarProps) {
  return (
    <nav
      className={`navbar ${
        darkMode
          ? 'navbar-dark bg-dark border-bottom border-secondary'
          : 'navbar-light bg-light border-bottom'
      } sticky-top`}
    >
      <div className="container-fluid d-flex justify-content-between align-items-center">
        <div className="d-flex align-items-center">
          <button className="navbar-toggler me-2" onClick={onToggleSidebar}>
            <span className="navbar-toggler-icon"></span>
          </button>
          <a className="navbar-brand me-3" href="#">
            OpsPilot | Dev Environment (Testing)
          </a>
          <a
            href="https://github.com/d4niee/OpsPilot"
            target="_blank"
            rel="noopener noreferrer"
            className="text-decoration-none"
            title="View Project on GitHub"
          >
            <FaGithub size={24} color={darkMode ? 'white' : 'black'} />
          </a>
        </div>
        <div>
          <Button
            variant="outline-secondary"
            className="me-2"
            onClick={toggleDarkMode}
          >
            {darkMode ? '☀️ Light' : '🌙 Dark'}
          </Button>
          <Button variant="outline-primary" onClick={onLogin}>
            Login
          </Button>
        </div>
      </div>
    </nav>
  );
}
