import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';
import { ToastNotificationProps } from '../types/ToastNotificationProps';

export default function ToastNotification({
  toast,
  darkMode,
}: ToastNotificationProps) {
  return (
    <ToastContainer position="bottom-center" className="p-3">
      <Toast
        show={toast.show}
        onClose={() => {}}
        delay={3000}
        autohide
        className={darkMode ? 'bg-dark text-white' : ''}
      >
        <Toast.Body>{toast.message}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}
