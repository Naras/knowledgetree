package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("scriptHome")
public class ScriptHome extends EntityHome<Script> {

	public void setScriptId(String id) {
		setId(id);
	}

	public String getScriptId() {
		return (String) getId();
	}

	@Override
	protected Script createInstance() {
		Script script = new Script();
		return script;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public Script getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<WorkInScript> getWorkInScripts() {
		return getInstance() == null ? null : new ArrayList<WorkInScript>(
				getInstance().getWorkInScripts());
	}

}
