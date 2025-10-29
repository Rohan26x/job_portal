import { AuthProvider } from '@/context/AuthContext';
import './globals.css';

export const metadata = {
  title: 'Job Portal - Find Your Dream Job',
  description: 'AI-powered job portal connecting recruiters and job seekers',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
