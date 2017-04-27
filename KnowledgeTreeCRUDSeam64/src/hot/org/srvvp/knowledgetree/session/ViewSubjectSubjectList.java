package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("viewSubjectSubjectList")
public class ViewSubjectSubjectList extends EntityQuery<ViewSubjectSubject> {

	private static final String EJBQL = "select viewSubjectSubject from ViewSubjectSubject viewSubjectSubject";

	private static final String[] RESTRICTIONS = {
			"lower(viewSubjectSubject.id.relation) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.relation},'%'))",
			"lower(viewSubjectSubject.id.relationDescription) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.relationDescription},'%'))",
			"lower(viewSubjectSubject.id.sub1id) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.sub1id},'%'))",
			"lower(viewSubjectSubject.id.sub2id) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.sub2id},'%'))",
			"lower(viewSubjectSubject.id.subject1) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.subject1},'%'))",
			"lower(viewSubjectSubject.id.subject1description) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.subject1description},'%'))",
			"lower(viewSubjectSubject.id.subject2) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.subject2},'%'))",
			"lower(viewSubjectSubject.id.subject2description) like lower(concat(#{viewSubjectSubjectList.viewSubjectSubject.id.subject2description},'%'))",};

	private ViewSubjectSubject viewSubjectSubject;

	public ViewSubjectSubjectList() {
		viewSubjectSubject = new ViewSubjectSubject();
		viewSubjectSubject.setId(new ViewSubjectSubjectId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public ViewSubjectSubject getViewSubjectSubject() {
		return viewSubjectSubject;
	}
}
