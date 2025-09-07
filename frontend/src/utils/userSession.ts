import { v4 as uuidv4 } from 'uuid';

const USER_ID_KEY = 'tuvi_user_id';

/**
 * Get or create user ID for session tracking
 */
export function getUserId(): string {
  // Try to get existing user ID from localStorage
  if (typeof window !== 'undefined') {
    const existingUserId = localStorage.getItem(USER_ID_KEY);
    if (existingUserId) {
      return existingUserId;
    }
    
    // Create new user ID if not exists
    const newUserId = uuidv4();
    localStorage.setItem(USER_ID_KEY, newUserId);
    return newUserId;
  }
  
  // Fallback for server-side rendering
  return uuidv4();
}

/**
 * Clear user ID (for new session)
 */
export function clearUserId(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(USER_ID_KEY);
  }
}

/**
 * Check if user has existing session
 */
export function hasExistingSession(): boolean {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(USER_ID_KEY) !== null;
  }
  return false;
}