import { usePlaidLink } from 'react-plaid-link';

const PlaidLinkComponent = ({ onSuccess }) => {
  const [linkToken, setLinkToken] = useState(null);
  
  useEffect(() => {
    // Fetch link token from backend
    fetch('/api/plaid/create_link_token', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    .then(res => res.json())
    .then(data => setLinkToken(data.link_token));
  }, []);
  
  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token, metadata) => {
      // Exchange public token for access token
      await fetch('/api/plaid/exchange_public_token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: JSON.stringify({ public_token, institution: metadata.institution })
      });
      onSuccess();
    },
  });
  
  return <button onClick={() => open()} disabled={!ready}>Connect Bank Account</button>;
};
