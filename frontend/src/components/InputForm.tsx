import { InputFormProps } from "../types/InputFormProps";

export default function InputForm({
  inputMessage,
  setInputMessage,
  onSubmit,
  darkMode,
}: InputFormProps) {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(inputMessage);
      }}
      className={`border-top border-secondary p-3 ${
        darkMode ? 'bg-dark text-white' : 'bg-white'
      } position-sticky bottom-0`}
    >
      <div className="input-group">
        <input
          type="text"
          className={`form-control ${
            darkMode ? 'bg-black text-white border-dark' : ''
          }`}
          placeholder="Type your message..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={!inputMessage.trim()}
        >
          Send
        </button>
      </div>
    </form>
  );
}
