import { createAgent } from 'langchain';
import { llm } from './llms';
import { mainAgentPrompt, postAnalystSubagentPrompt } from './prompts';
import {
	callPostAnalystSubagent,
	getAllPlayerTypologies,
	getPlayerTypologyInformationByName,
	savePostToDB
} from './tools';

export const agent = createAgent({
	model: llm,
	tools: [callPostAnalystSubagent],
	systemPrompt: mainAgentPrompt
});

export const postAnalystSubagent = createAgent({
	model: llm,
	tools: [savePostToDB, getAllPlayerTypologies, getPlayerTypologyInformationByName],
	systemPrompt: postAnalystSubagentPrompt
});
