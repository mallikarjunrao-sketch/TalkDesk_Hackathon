# Talkdesk Hackathon Sandbox Findings

**Project:** PULSE --- Refund Verification and Incident Intelligence\
**Environment:** PESIT Talkdesk Hackathon sandbox\
**Finding status:** Based on the sandbox screens and navigation explored
so far

------------------------------------------------------------------------

## 1. Executive summary

The Talkdesk sandbox provides access to the **AI Agent Platform**,
including **MCP Servers**. The sandbox also exposes **Studio**,
**Automation Flows**, **Integrations**, and **Workspace Designer** in
the navigation.

The most promising integration path for PULSE is a **custom MCP server**
connected to the Talkdesk AI Agent Platform. The sandbox exposes a form
to register a custom MCP server, but the end-to-end connection and agent
invocation still need to be tested.

## 2. Features observed

  -----------------------------------------------------------------------
  Feature                 Finding                 Evidence / notes
  ----------------------- ----------------------- -----------------------
  AI Agent Platform       Available               Visible in the main
                                                  navigation.

  AI Agent Orchestration  Available               Visible as a section
                                                  under AI Agent
                                                  Platform.

  MCP Servers             Available               Visible under AI Agent
                                                  Platform.

  Create custom MCP       Available               The New MCP Server flow
  Server                                          includes an **Add
                                                  custom** option.

  MCP server              Available               Form includes Name,
  configuration form                              Description, Status,
                                                  URL, Authentication,
                                                  Test connection, Save,
                                                  and Cancel.

  Agent Evaluation        Available               Visible under AI Agent
                                                  Platform.

  Agent Observability     Available               Visible under AI Agent
                                                  Platform.

  Studio                  Available               Visible in the main
                                                  navigation.

  Automation Flows        Available               Visible in the main
                                                  navigation.

  Integrations            Available               Appeared in the sandbox
                                                  search/navigation.

  Workspace Designer /    Available               Workspace Designer is
  Custom Workspace                                visible; Custom
                                                  Workspace was observed.

  Webhooks                Not located             Searching the sandbox
                                                  for "webhooks" did not
                                                  reveal a matching
                                                  feature. This does
                                                  **not** prove webhooks
                                                  are disabled.

  Copilot                 Not located             Searching the sandbox
                                                  for "copilot" did not
                                                  reveal a matching
                                                  feature. This does
                                                  **not** prove Copilot
                                                  is disabled.
  -----------------------------------------------------------------------

## 3. Custom MCP server form

The **Add custom MCP Server** form showed these fields:

-   **Name** --- required
-   **Description** --- required
-   **Status** --- enable/disable toggle
-   **URL** --- required; placeholder showed an HTTPS MCP-style URL
-   **Authentication** --- dropdown, initially set to `None`
-   **Test connection** --- button
-   **Save** and **Cancel** --- actions

This is sufficient to begin configuring a custom MCP server, subject to
validating the endpoint protocol and authentication requirements with
the sandbox's connection test.

## 4. Recommended PULSE integration approach

### Preferred path: custom MCP server

Build a small MCP server owned by the Talkdesk integration workstream.
It should expose PULSE backend capabilities as MCP tools and call the
team's FastAPI backend.

For the first integration milestone, start with one simple tool:

-   `check_backend_health` --- calls the PULSE backend health endpoint
    and returns the backend's actual response.

Suggested local development arrangement:

  ------------------------------------------------------------------------
  Component                     Suggested local port Purpose
  --------------------- ---------------------------- ---------------------
  PULSE FastAPI backend                       `8000` Backend API, owned by
                                                     the backend
                                                     workstream

  PULSE MCP server                            `8001` MCP tools exposed to
                                                     Talkdesk

  Public tunnel         Provider-assigned HTTPS port Makes the MCP
                                             mapping endpoint reachable
                                                     from Talkdesk
  ------------------------------------------------------------------------

The MCP server endpoint may be exposed locally at:

``` text
http://127.0.0.1:8001/mcp
```

For a remote Talkdesk sandbox, expose port `8001` through a temporary
HTTPS tunnel and register the resulting public MCP URL, ending in
`/mcp`, in the Talkdesk form.

**Important:** A normal REST endpoint such as `/health` is not itself an
MCP endpoint. Talkdesk must be given the URL of the MCP server, not the
FastAPI health URL. The MCP tool can call the REST health endpoint
internally.

### Backend location consideration

If the FastAPI backend runs on a teammate's laptop, `127.0.0.1:8000`
from the MCP server's laptop will refer to the MCP server's own machine,
not the teammate's machine. Use a reachable backend URL, such as an
accessible LAN address or a separately exposed HTTPS endpoint, after
coordinating with the backend owner.

## 5. Suggested first test (G1)

The first goal should be a small, demonstrable end-to-end interaction:

1.  Confirm the PULSE backend health endpoint is reachable from the
    machine running the MCP server.
2.  Start the MCP server and verify that its `check_backend_health` tool
    returns the backend response.
3.  Expose the MCP endpoint through HTTPS so the Talkdesk sandbox can
    reach it.
4.  Enter the public MCP URL in the Talkdesk **Add custom MCP Server**
    form.
5.  Select **Test connection** and save only after the connection test
    succeeds.
6.  Configure a Talkdesk AI agent to use the health-check tool.
7.  Run a real Talkdesk conversation and verify that the agent invokes
    the tool and presents the backend's returned response.

A successful MCP server connection test alone does not complete G1. G1
requires a real Talkdesk interaction to invoke the backend through the
integration and show the backend response.

## 6. Integration fallback order

If the custom MCP route cannot be completed, investigate alternatives in
this order:

1.  **Integration / Workflow skill** --- check whether the sandbox
    supports a suitable integration or workflow action.
2.  **Studio webhook** --- use only if a webhook capability and the
    required configuration are actually available.
3.  **Thin `/chat` fallback** --- use as a last-resort demo path if the
    preferred Talkdesk integration routes are blocked, and clearly
    describe what is and is not native.

Do not claim a webhook or Copilot capability is unavailable solely
because it was not found in search. Record it as **not located / not
verified** until tested or confirmed by the sandbox administrator.

## 7. Current status and open checks

### Confirmed from the sandbox exploration

-   [x] AI Agent Platform is visible.
-   [x] MCP Servers is visible.
-   [x] The custom MCP server creation flow is available.
-   [x] The custom MCP form includes a URL field and a Test connection
    action.
-   [x] Studio is visible.
-   [x] Automation Flows is visible.
-   [x] Integrations is discoverable.
-   [x] Workspace Designer / Custom Workspace is visible.

### Not yet verified

-   [ ] A custom MCP server can successfully connect from the Talkdesk
    sandbox.
-   [ ] The sandbox accepts the proposed Streamable HTTP MCP transport.
-   [ ] Authentication requirements for the custom MCP endpoint.
-   [ ] A Talkdesk AI agent can select and invoke the registered MCP
    tool.
-   [ ] The tool can reach the team's actual FastAPI backend.
-   [ ] The complete Talkdesk-to-MCP-to-backend interaction succeeds.
-   [ ] Studio webhook availability and configuration.
-   [ ] Whether Copilot is enabled for this sandbox.
-   [ ] Whether Custom Workspace supports creating and deploying a
    custom app for this use case.

## 8. Demo integrity and claims

For the PULSE demo, distinguish real integrations from simulated
systems:

-   Talkdesk conversation and agent interaction: claim as real only
    after tested.
-   MCP server and backend calls: claim as real only after end-to-end
    verification.
-   Policy engine, refund executor, independent verifier, commitment
    ledger, and incident correlator: describe according to what the team
    has actually implemented and tested.
-   Payment gateway, bank settlement, reconciliation feed, and customer
    data: label as simulated where applicable.

Do not state that a refund is **VERIFIED** merely because a refund
request was accepted. PULSE's central claim is that verification
requires an independent settlement check.

## 9. Immediate next action

Build and run the minimal MCP server with one `check_backend_health`
tool, test it locally, and then register its public HTTPS `/mcp`
endpoint in the Talkdesk sandbox. After the connection test, configure
an AI agent and verify a real tool invocation.

------------------------------------------------------------------------

**Document note:** These findings describe the sandbox UI that was
inspected. Items marked "not located" or "not yet verified" should not
be treated as proof that the capability is disabled.
