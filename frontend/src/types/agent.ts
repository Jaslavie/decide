/**
 * Type definition for agents (shared with the backend)
 */

export interface Agent {
    name: string;
    role: string;
    status: 'idle' | 'processing' | 'error';
}

export interface AgentMessage {
    fromAgent: string;
    toAgent: string;
    content: any;
    metadata: {
        timestamp: number;
        priority: number;
    }
}