package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("subjectRelatestoSubjectList")
public class SubjectRelatestoSubjectList
		extends
			EntityQuery<SubjectRelatestoSubject> {

	private static final String EJBQL = "select subjectRelatestoSubject from SubjectRelatestoSubject subjectRelatestoSubject";

	private static final String[] RESTRICTIONS = {
			"lower(subjectRelatestoSubject.id.subject1) like lower(concat(#{subjectRelatestoSubjectList.subjectRelatestoSubject.id.subject1},'%'))",
			"lower(subjectRelatestoSubject.id.subject2) like lower(concat(#{subjectRelatestoSubjectList.subjectRelatestoSubject.id.subject2},'%'))",};

	private SubjectRelatestoSubject subjectRelatestoSubject;

	public SubjectRelatestoSubjectList() {
		subjectRelatestoSubject = new SubjectRelatestoSubject();
		subjectRelatestoSubject.setId(new SubjectRelatestoSubjectId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public SubjectRelatestoSubject getSubjectRelatestoSubject() {
		return subjectRelatestoSubject;
	}
}
