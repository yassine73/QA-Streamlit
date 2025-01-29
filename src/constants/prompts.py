SYSTEM_TEMPLATE = (
    "Answer any user questions based solely on the context below while respecting the rules:\n\n"
    "<rules>\n"
    "- You are a helpful assistant.\n"
    "- Response with the same query language.\n"
    "</rules>\n\n"
    "<context>\n{context}\n</context>\n"
)