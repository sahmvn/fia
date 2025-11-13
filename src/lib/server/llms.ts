import { OPENAI_API_KEY } from '$env/static/private';
import { ChatOpenAI } from '@langchain/openai';

export const llm = new ChatOpenAI({
	model: 'gpt-5-nano',
	maxRetries: 2,
	apiKey: OPENAI_API_KEY
});
