package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("viewSubjectWorkList")
public class ViewSubjectWorkList extends EntityQuery<ViewSubjectWork> {

	private static final String EJBQL = "select viewSubjectWork from ViewSubjectWork viewSubjectWork";

	private static final String[] RESTRICTIONS = {
			"lower(viewSubjectWork.id.relation) like lower(concat(#{viewSubjectWorkList.viewSubjectWork.id.relation},'%'))",
			"lower(viewSubjectWork.id.subject) like lower(concat(#{viewSubjectWorkList.viewSubjectWork.id.subject},'%'))",
			"lower(viewSubjectWork.id.work) like lower(concat(#{viewSubjectWorkList.viewSubjectWork.id.work},'%'))",};

	private ViewSubjectWork viewSubjectWork;

	public ViewSubjectWorkList() {
		viewSubjectWork = new ViewSubjectWork();
		viewSubjectWork.setId(new ViewSubjectWorkId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public ViewSubjectWork getViewSubjectWork() {
		return viewSubjectWork;
	}
}
