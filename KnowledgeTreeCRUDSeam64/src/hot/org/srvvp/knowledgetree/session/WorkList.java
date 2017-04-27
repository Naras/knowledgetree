package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workList")
public class WorkList extends EntityQuery<Work> {

	private static final String EJBQL = "select work from Work work";

	private static final String[] RESTRICTIONS = {
			"lower(work.id) like lower(concat(#{workList.work.id},'%'))",
			"lower(work.description) like lower(concat(#{workList.work.description},'%'))",
			"lower(work.title) like lower(concat(#{workList.work.title},'%'))",};

	private Work work = new Work();

	public WorkList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Work getWork() {
		return work;
	}
}
