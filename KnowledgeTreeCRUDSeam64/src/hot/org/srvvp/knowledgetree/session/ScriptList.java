package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("scriptList")
public class ScriptList extends EntityQuery<Script> {

	private static final String EJBQL = "select script from Script script";

	private static final String[] RESTRICTIONS = {
			"lower(script.id) like lower(concat(#{scriptList.script.id},'%'))",
			"lower(script.name) like lower(concat(#{scriptList.script.name},'%'))",};

	private Script script = new Script();

	public ScriptList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Script getScript() {
		return script;
	}
}
