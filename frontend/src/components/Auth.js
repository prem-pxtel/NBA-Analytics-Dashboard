import React, { useState } from 'react';

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true); // false means isSignup
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [inviteCode, setInviteCode] = useState('');


  const handleSubmit = async (e) => {
    e.preventDefault();

    const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
    const body = isLogin ? { username, password } : { username, password, invite_code: inviteCode };

    try {
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
      });

      const responseData = await response.json();

      if (response.ok) {
        if (isLogin || true) {
          localStorage.setItem('access_token', responseData.access_token);
          onLogin(responseData.access_token);
        } else {
          setIsLogin(true);
        }
      }
    } catch (err) {
      alert("An error occured, try again later")
      console.log(err)
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '100px auto', padding: '20px' }}>
      <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ width: '100%', padding: '10px', fontSize: '16px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '10px', fontSize: '16px' }}
          />
        </div>

        {!isLogin && (
          <div style={{ marginBottom: '10px' }}>
            <input
              placeholder="Invite Code (optional)"
              value={inviteCode}
              onChange={(e) => setInviteCode(e.target.value)}
              style={{ width: '100%', padding: '10px', fontSize: '16px' }}
            />
          </div>
        )}

        <button
          type="submit"
          style={{ 
            width: '100%', 
              padding: '10px', 
  fontSize: '16px',
  backgroundColor: '#7fcdee',
      color: 'white',
    }}
        >
                {isLogin ? 'Login' : 'Sign Up'}
              </button>
            </form>

      <p >
        {isLogin ? "New here? " : "Not your first time? "}
            <button
      type="button"
      onClick={() => {
        setIsLogin(!isLogin);
          }}
  >
    {isLogin ? 'Sign up' : 'Login'}
  </button>
      </p>
    </div>
  );
}

export default Auth; 