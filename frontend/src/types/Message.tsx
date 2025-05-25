export interface Message {
  id: number;
  text: string;
  isBot: boolean;
  buttons?: { title: string; payload: string }[];
}