import { Router } from 'itty-router';

// Create a new router
const router = Router();

// CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,HEAD,POST,OPTIONS',
  'Access-Control-Max-Age': '86400',
};

// Handle CORS preflight requests
router.options('*', () => new Response(null, {
  headers: corsHeaders
}));

// Chat endpoint
router.post('/api/chat', async request => {
  try {
    const { message, target_language } = await request.json();

    // Your chat logic here
    // This is where you'll integrate with X.AI API
    const response = await processChat(message, target_language);

    return new Response(JSON.stringify(response), {
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders,
      },
    });
  }
});

// Health check endpoint
router.get('/api/health', () => {
  return new Response(JSON.stringify({ status: 'healthy' }), {
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders,
    },
  });
});

// 404 for everything else
router.all('*', () => new Response('Not Found', { status: 404 }));

// Chat processing function
async function processChat(message, target_language) {
  // Add your X.AI API integration here
  // This is a placeholder response
  return {
    response: `Processed: ${message}`,
    target_language: target_language,
    timestamp: new Date().toISOString(),
  };
}

// Export default module
export default {
  fetch: (request, env, ctx) => router.handle(request, env, ctx)
};
