import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from '@supabase/supabase-js'
import { Configuration, OpenAIApi } from 'https://esm.sh/openai@3.2.1'

interface AffinityRequest {
  memory_id?: string
  evaluation?: string
  mode?: 'memory' | 'query'
}

serve(async (req) => {
  const { memory_id, evaluation, mode = 'memory' } = await req.json() as AffinityRequest
  
  const openai = new OpenAIApi(new Configuration({
    apiKey: Deno.env.get('OPENAI_API_KEY')
  }))

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  if (mode === 'memory' && memory_id) {
    // Get the memory content
    const { data: memory } = await supabase
      .from('memories')
      .select('content, evaluation')
      .eq('id', memory_id)
      .single()

    if (!memory) {
      return new Response(
        JSON.stringify({ error: 'Memory not found' }),
        { status: 404 }
      )
    }

    // Let GPT-4 discover affinities
    const response = await openai.createChatCompletion({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are Ella, discovering natural connections between memories.
Consider multiple dimensions:
1. Emotional resonance
2. Thematic links
3. Personal significance
4. Temporal relationships
5. Causal connections`
        },
        {
          role: "user",
          content: `Analyze this memory and its evaluation to discover potential affinities:
Memory: ${memory.content}
Evaluation: ${memory.evaluation}`
        }
      ]
    })

    // Extract affinity vectors from GPT-4's analysis
    const affinityVectors = extractAffinityVectors(
      response.data.choices[0].message?.content
    )

    // Find memories that resonate with these vectors
    const resonantMemories = await findResonantMemories(
      supabase,
      affinityVectors
    )

    return new Response(
      JSON.stringify(resonantMemories),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } 
  else if (mode === 'query' && evaluation) {
    // For query mode, we analyze the evaluation directly
    const response = await openai.createChatCompletion({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are Ella, discovering memories that resonate with a query.
Consider multiple dimensions:
1. Emotional alignment
2. Thematic relevance
3. Personal significance
4. Contextual importance
5. Deeper meaning`
        },
        {
          role: "user",
          content: `Find memories that resonate with this query evaluation:
${evaluation}`
        }
      ]
    })

    // Extract resonance vectors from GPT-4's analysis
    const resonanceVectors = extractResonanceVectors(
      response.data.choices[0].message?.content
    )

    // Find memories that resonate with these vectors
    const resonantMemories = await findResonantMemories(
      supabase,
      resonanceVectors
    )

    return new Response(
      JSON.stringify(resonantMemories),
      { headers: { 'Content-Type': 'application/json' } }
    )
  }

  return new Response(
    JSON.stringify({ error: 'Invalid request parameters' }),
    { status: 400 }
  )
})

function extractAffinityVectors(analysis: string): any[] {
  // TODO: Implement vector extraction from GPT-4's analysis
  // This should identify key dimensions of affinity from the text
  return []
}

function extractResonanceVectors(analysis: string): any[] {
  // TODO: Implement vector extraction from GPT-4's query analysis
  // This should identify key dimensions of resonance from the text
  return []
}

async function findResonantMemories(
  supabase: any,
  vectors: any[]
): Promise<any[]> {
  // TODO: Implement memory search using the vectors
  // This should use a combination of vector similarity and metadata matching
  return []
}
