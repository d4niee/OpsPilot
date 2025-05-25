export interface InputFormProps {
  inputMessage: string;
  setInputMessage: (msg: string) => void;
  onSubmit: (msg: string) => void;
  darkMode: boolean;
}
