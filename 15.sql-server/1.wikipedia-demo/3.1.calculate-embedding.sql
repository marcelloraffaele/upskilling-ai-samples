-- Calculate embeddings for all titles in wikipedia_articles_embeddings
declare @embedding vector(1536);

declare cur cursor for
    select id, title from dbo.wikipedia_articles_embeddings;

declare @id int, @title nvarchar(max);

open cur;
fetch next from cur into @id, @title;

while @@fetch_status = 0
begin
    exec dbo.get_embedding
        @deployedModelName = N'text-embedding-ada-002', -- replace with your model deployment name
        @inputText = @title,
        @embedding = @embedding output;

    update dbo.wikipedia_articles_embeddings
    set title_vector_ada2 = cast(@embedding as varchar(max))
    where id = @id;

    fetch next from cur into @id, @title;
end

close cur;
deallocate cur;

---------------
declare @embedding vector(1536);

declare cur cursor for
    select id, text from dbo.wikipedia_articles_embeddings;

declare @id int, @text nvarchar(max);

open cur;
fetch next from cur into @id, @text;

while @@fetch_status = 0
begin
    exec dbo.get_embedding
        @deployedModelName = N'text-embedding-ada-002', -- replace with your model deployment name
        @inputText = @text,
        @embedding = @embedding output;

    update dbo.wikipedia_articles_embeddings
    set content_vector_ada2 = cast(@embedding as varchar(max))
    where id = @id;

    fetch next from cur into @id, @text;
end

close cur;
deallocate cur;
