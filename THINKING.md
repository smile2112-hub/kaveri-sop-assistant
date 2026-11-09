# Thinking

## Understand the user

The primary user is a shift supervisor or experienced operator on a manufacturing shop floor. They may be moving between machines, wearing gloves, using a phone or shared tablet, and trying to make a safe decision without leaving production. They need a short answer to questions such as an alarm meaning, a measurement limit, who owns a maintenance task, or what the next procedural step is.

Their current frustrations are likely:

- searching long PDFs or a QMS from a noisy shop floor;
- uncertainty about which revision is current;
- procedures using different terms for operators, authorised persons, QC roles, and maintenance roles;
- needing the practical action, not just a definition;
- poor connectivity, small screens, and limited time;
- the risk of confidently acting on an answer that is not actually in the controlled documents.

Assumptions: the supervisor is authenticated elsewhere in a real deployment, has permission to see plant procedures, and treats this copilot as a document lookup aid rather than an authority that replaces the QMS or a safety escalation.

## User journey

1. The supervisor notices a machine alarm or a question during a shift.
2. They open the copilot on a phone or shared tablet.
3. They type a plain-language question, such as “What does AL-104 mean?”
4. The copilot searches the maintenance, quality, and safety documents.
5. It shows a concise excerpt, the source document, and enough context to act.
6. The supervisor checks that the source is the expected procedure and follows the stated action.
7. For a safety-critical or unusual situation, they contact the responsible person and check the controlled QMS copy.
8. If no document supports the question, the copilot says that it does not know and points the user to a supervisor/QMS rather than guessing.

Things that could go wrong:

- the user asks an ambiguous question (“the lock”) or uses a local abbreviation;
- a retrieved passage comes from an obsolete revision;
- two documents conflict;
- the answer is technically correct but omits an important safety precondition;
- a PDF was scanned and its text was not extracted;
- the phone loses connectivity or the API is unavailable;
- a user trusts an answer beyond the scope of the documents;
- the search finds a related phrase but not the actual answer, creating false confidence.

## AI challenge

I asked an AI reviewer to be skeptical:

> **Reviewer:** What is the most dangerous failure mode in this journey?
>
> **Me:** A plausible-looking answer from the wrong revision or a partial safety passage. The user may act before checking the source.
>
> **Reviewer:** Then why does a source filename alone create enough trust? How will a user know whether the answer is current, and what happens when nothing matches?
>
> **Me:** It does not create enough trust. The interface needs an explicit source, a not-found state, and a reminder that urgent decisions should use the controlled QMS.
>
> **Reviewer:** Also challenge the assumption that a supervisor will type a perfect question. A mobile flow should provide example prompts and tolerate ordinary wording. Retrieval should be conservative rather than always producing a best match.
>
> **Me:** Agreed. I added prompt suggestions, a responsive layout, basic term-overlap retrieval, and a threshold that returns “not found” instead of a weak match.

I agreed with the critique about false confidence, revision visibility, and the need for a clear no-answer path. I did not treat a filename as a full document-control solution; it is only a useful first step in this five-hour assignment. I also kept the implementation extractive and small so a reviewer can see why a passage was returned. In production I would add document metadata, current-revision filtering, access control, and a stronger evaluation set.

## The improvement I added, and why I chose it

The improvement is **safe abstention with source visibility**. Every supported response identifies the source file, while a weak or unrelated match returns an explicit “I couldn't find that in the plant documents” response with no source. The UI also includes a short warning to use the controlled QMS and contact a supervisor for urgent safety decisions.

I chose this because the user journey's most costly failure is an invented or weakly supported instruction. A polished answer is less valuable than an honest boundary in a safety and quality context. The same change is testable: the app must return a source for known questions and no source for the cafeteria question.

## Final reflection

The biggest challenge was that the sample PDFs were not available in the local assignment folder. I handled that by preserving the supplied document content as clearly named text source files, documenting the limitation, and implementing a loader that also supports real PDFs through `pypdf`. This keeps the app runnable without pretending that a PDF was downloaded.

Next I would build a proper ingestion pipeline: extract text and tables, preserve page numbers and revision/effective-date metadata, chunk by section, embed chunks in a vector store, and filter to the current approved revision. I would add citations down to page and section, feedback buttons, query/audit logs, offline-friendly caching, and role-based access.

I am still unsure how the plant handles controlled-document updates, whether supervisors need Tamil or other local-language support, how often connectivity fails, and whether users should be able to search only their own area. I would ask the customer:

- Which system is the source of truth for document revisions?
- What response time and offline behavior are acceptable?
- Which questions must always escalate to a person?
- Which users can see safety, quality, and maintenance procedures?
- What existing alarm and machine identifiers should be included?

The local-network deployment is intentionally simple: Uvicorn binds to `0.0.0.0`, and a phone on the same Wi-Fi uses the laptop's private IPv4 address. A real deployment would put the service behind HTTPS, authentication, network controls, monitoring, and a managed document store rather than exposing a development server.
