import { useState } from "react";
import ChatHeader from "@/components/ChatHeader";
import ChatMessage from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";
import WelcomeScreen from "@/components/WelcomeScreen";
import Sidebar from "@/components/Sidebar";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  analysis?: {
    findings: Array<{
      type: "warning" | "danger" | "info";
      title: string;
      description: string;
    }>;
  };
}

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string>("1");
  const [chatHistory, setChatHistory] = useState([
    { id: "1", title: "My current relationship concerns", timestamp: new Date(2025, 0, 15) },
    { id: "2", title: "Past relationship patterns", timestamp: new Date(2025, 0, 10) },
    { id: "3", title: "Friend's situation analysis", timestamp: new Date(2025, 0, 5) },
  ]);
  const { toast } = useToast();

  // Mock analysis function - replace with actual API call
  const analyzeStory = async (text: string): Promise<Message> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 3000));

    // Mock analysis results
    return {
      id: Date.now().toString(),
      role: "assistant",
      content: `I've analyzed your relationship story and found matching patterns in several movie scripts. Here's what I discovered:`,
      analysis: {
        findings: [
          {
            type: "danger",
            title: "Power Imbalance - Similar to 'Gaslight' (1944)",
            description:
              "Your story shows a significant power differential where your partner controls decisions and limits your autonomy, mirroring the classic manipulation depicted in this film.",
          },
          {
            type: "warning",
            title: "Reality Questioning - Pattern from 'Sleeping with the Enemy' (1991)",
            description:
              "The instances where your partner questions your perception match gaslighting tactics seen in this thriller, designed to make you doubt yourself.",
          },
          {
            type: "danger",
            title: "Isolation Tactics - 'The Invisible Man' (2020)",
            description:
              "Your description of being separated from friends and family mirrors isolation behaviors used by abusers to gain control.",
          },
          {
            type: "info",
            title: "Your Strength - You're Recognizing Patterns",
            description: "The fact that you're here seeking clarity shows self-awareness. This is the first step toward empowerment.",
          },
        ],
      },
    };
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const assistantMessage = await analyzeStory(content);
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      toast({
        title: "Analysis Error",
        description: "Failed to analyze the script. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    const newId = (chatHistory.length + 1).toString();
    setChatHistory([
      { id: newId, title: "New conversation", timestamp: new Date() },
      ...chatHistory,
    ]);
    setCurrentChatId(newId);
    setMessages([]);
  };

  const handleSelectChat = (id: string) => {
    setCurrentChatId(id);
    setMessages([]);
  };

  const handleDeleteChat = (id: string) => {
    setChatHistory(chatHistory.filter((chat) => chat.id !== id));
    if (currentChatId === id) {
      setCurrentChatId(chatHistory[0]?.id || "");
      setMessages([]);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <ChatHeader />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          chatHistory={chatHistory}
          currentChatId={currentChatId}
          onSelectChat={handleSelectChat}
          onNewChat={handleNewChat}
          onDeleteChat={handleDeleteChat}
        />

        <main className="flex-1 flex flex-col overflow-hidden">
        {messages.length === 0 ? (
          <WelcomeScreen />
        ) : (
          <div className="flex-1 overflow-y-auto">
            <div className="container mx-auto px-4 py-8">
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex justify-start mb-6">
                  <div className="bg-card border border-border rounded-2xl px-5 py-4 shadow-medium">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <div className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "0ms" }} />
                        <div className="h-2 w-2 rounded-full bg-accent animate-bounce" style={{ animationDelay: "150ms" }} />
                        <div className="h-2 w-2 rounded-full bg-secondary animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                      <span className="text-sm text-muted-foreground">Analyzing script...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </main>
      </div>
    </div>
  );
};

export default Index;
