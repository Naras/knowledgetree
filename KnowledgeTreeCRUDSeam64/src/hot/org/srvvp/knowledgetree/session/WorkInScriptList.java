package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workInScriptList")
public class WorkInScriptList extends EntityQuery<WorkInScript> {

	private static final String EJBQL = "select workInScript from WorkInScript workInScript";

	private static final String[] RESTRICTIONS = {
			"lower(workInScript.id.script) like lower(concat(#{workInScriptList.workInScript.id.script},'%'))",
			"lower(workInScript.id.work) like lower(concat(#{workInScriptList.workInScript.id.work},'%'))",
			"lower(workInScript.location) like lower(concat(#{workInScriptList.workInScript.location},'%'))",};

	private WorkInScript workInScript;

	public WorkInScriptList() {
		workInScript = new WorkInScript();
		workInScript.setId(new WorkInScriptId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public WorkInScript getWorkInScript() {
		return workInScript;
	}
}
