import Offcanvas from 'react-bootstrap/Offcanvas';
import ListGroup from 'react-bootstrap/ListGroup';

interface SidebarProps {
  show: boolean;
  onHide: () => void;
  darkMode: boolean;
}

export default function SideBar({
  show,
  onHide,
  darkMode,
}: SidebarProps) {
  return (
    <Offcanvas
      show={show}
      onHide={onHide}
      placement="start"
      className={`border-end ${
        darkMode ? 'bg-dark text-white' : ''
      }`}
      style={{ width: 280 }}
    >
      <Offcanvas.Header
        className={darkMode ? 'bg-dark' : ''}
        closeVariant={darkMode ? 'white' : undefined}
      >
        <Offcanvas.Title>📖 Chat History</Offcanvas.Title>
      </Offcanvas.Header>
      <Offcanvas.Body className="p-0">
        <ListGroup variant="flush">
          {[1, 2, 3].map((i) => (
            <ListGroup.Item
              key={i}
              action
              className={darkMode ? 'bg-dark text-white' : ''}
            >
              Sample Entry {i}
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Offcanvas.Body>
    </Offcanvas>
  );
}
