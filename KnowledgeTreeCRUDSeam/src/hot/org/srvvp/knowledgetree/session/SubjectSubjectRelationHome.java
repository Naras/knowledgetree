package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("subjectSubjectRelationHome")
public class SubjectSubjectRelationHome
		extends
			EntityHome<SubjectSubjectRelation> {

	public void setSubjectSubjectRelationId(String id) {
		setId(id);
	}

	public String getSubjectSubjectRelationId() {
		return (String) getId();
	}

	@Override
	protected SubjectSubjectRelation createInstance() {
		SubjectSubjectRelation subjectSubjectRelation = new SubjectSubjectRelation();
		return subjectSubjectRelation;
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

	public SubjectSubjectRelation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<SubjectRelatestoSubject> getSubjectRelatestoSubjects() {
		return getInstance() == null
				? null
				: new ArrayList<SubjectRelatestoSubject>(getInstance()
						.getSubjectRelatestoSubjects());
	}

}
