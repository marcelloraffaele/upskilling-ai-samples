/*
    Get the embeddings for the input text by calling the OpenAI API
    and then search the most similar articles (by title)
    Note: <deployment-id> needs to be replaced with the deployment name of your embedding model in Azure OpenAI
*/

declare @inputText nvarchar(max) = 'Linux operating system kernel';
declare @retval int, @embedding vector(1536);

exec @retval = dbo.get_embedding 'text-embedding-ada-002', @inputText, @embedding output;

select top(10)
    a.id,
    a.title,
    a.url,
    vector_distance('cosine', @embedding, content_vector_ada2) cosine_distance
from
    dbo.wikipedia_articles_embeddings a
order by
    cosine_distance;
go
