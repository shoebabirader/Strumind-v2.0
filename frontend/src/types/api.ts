// API Response wrapper
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  status?: string;
  success?: boolean;
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Error response
export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}
