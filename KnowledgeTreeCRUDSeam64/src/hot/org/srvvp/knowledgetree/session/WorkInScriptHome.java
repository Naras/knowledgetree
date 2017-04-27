package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workInScriptHome")
public class WorkInScriptHome extends EntityHome<WorkInScript> {

	@In(create = true)
	ScriptHome scriptHome;
	@In(create = true)
	WorkHome workHome;

	public void setWorkInScriptId(WorkInScriptId id) {
		setId(id);
	}

	public WorkInScriptId getWorkInScriptId() {
		return (WorkInScriptId) getId();
	}

	public WorkInScriptHome() {
		setWorkInScriptId(new WorkInScriptId());
	}

	@Override
	public boolean isIdDefined() {
		if (getWorkInScriptId().getScript() == null
				|| "".equals(getWorkInScriptId().getScript()))
			return false;
		if (getWorkInScriptId().getWork() == null
				|| "".equals(getWorkInScriptId().getWork()))
			return false;
		return true;
	}

	@Override
	protected WorkInScript createInstance() {
		WorkInScript workInScript = new WorkInScript();
		workInScript.setId(new WorkInScriptId());
		return workInScript;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Script script = scriptHome.getDefinedInstance();
		if (script != null) {
			getInstance().setScript(script);
		}
		Work work = workHome.getDefinedInstance();
		if (work != null) {
			getInstance().setWork(work);
		}
	}

	public boolean isWired() {
		if (getInstance().getScript() == null)
			return false;
		if (getInstance().getWork() == null)
			return false;
		return true;
	}

	public WorkInScript getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
