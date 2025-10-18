export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  organization?: string;
  license_type?: 'trial' | 'professional' | 'enterprise';
  created_at?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
  organization?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  expires_in?: number;
}

export interface DisclaimerAcceptance {
  user_id: number;
  accepted: boolean;
  timestamp: string;
  ip_address?: string;
}
